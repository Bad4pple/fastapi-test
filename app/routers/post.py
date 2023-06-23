from fastapi import APIRouter, status, Depends,HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db 
from app import schemas, models, oauth2
from typing import List

router = APIRouter(prefix="/post", tags=["Post"])

@router.get("/", status_code=status.HTTP_200_OK)
async def get_posts(db: Session = Depends(get_db), limit: int = 5, skip: int = 1, search: str = ""):
    # print(search)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()
    # result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    # return result
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts_dict = []
    for post, vote_count in posts:
        post_dict = post.__dict__
        post_dict["votes"] = vote_count
        posts_dict.append(post_dict)

    return posts_dict
    # return posts

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), get_current_user: schemas.TokenData = Depends(oauth2.get_current_user)):

    new_post = models.Post(title=post.title, content=post.content, published=post.published, owner_id=get_current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

@router.get("/{post_id}",status_code=status.HTTP_200_OK, response_model=schemas.Post,)
async def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post's id not {post_id} found")
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db), get_current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post's id not {post_id} found")
    if get_current_user.id != post.first().owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"permission denied you can not delete another post")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}")
async def update_post(post_id: int, post_request: schemas.PostBase, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == post_id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post's {post_id} id not found")
    
    post_query.update(post_request.dict(), synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_200_OK)