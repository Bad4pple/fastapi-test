from fastapi import APIRouter
from app.routers import post, user, auth, votes

router = APIRouter(prefix="/api")


router.include_router(router=auth.router)
router.include_router(router=post.router)
router.include_router(router=user.router)
router.include_router(router=votes.router)