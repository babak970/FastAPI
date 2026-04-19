from sqlalchemy import func

from .. import models, schemas , utils
from fastapi import FastAPI , Response , status , HTTPException , Depends , Request, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from typing import Optional,List
from .. import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)
#get all posts
@router.get("/",response_model=List[schemas.PostOut])
def posts(db:Session=Depends(get_db),limit : int = 10 , skip : int = 0,search : Optional[str] =  "" ):
        posts = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote , models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()



        print(posts)
        return  posts
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def posts(post: schemas.BasePost, db:Session=Depends(get_db) ,current_user : int = Depends(oauth2.get_current_user)):
    # print(current_user.email)
    new_post = models.Post(**post.model_dump(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#get post by id
@router.get("/{id}", response_model=schemas.PostOut)
def get_post( id : int ,db:Session=Depends(get_db) ,current_user : int = Depends(oauth2.get_current_user)):
    try:
        post = (db.query(models.Post , func.count(models.Vote.post_id).label("votes"))
                .join(models.Vote , models.Vote.post_id == models.Post.id,isouter=True)
                .group_by(models.Post.id).filter(models.Post.id == id).first())
        if not post:
            raise HTTPException(status.HTTP_404_NOT_FOUND,  f"post with {id} not founwaqweqweqwwewwd")
    except Exception as error:
        return {"error": error}
    return  post

@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session=Depends(get_db), current_user : int = Depends(oauth2.get_current_user) ):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"post with {id} not authorized")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def put_post(id: int,updated_post : schemas.Post,db:Session=Depends(get_db),current_user : int = Depends(oauth2.get_current_user) ):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post  == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"post with {id} not authorized")
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return {"data" : updated_post}

