from fastapi import APIRouter ,Depends , status , HTTPException ,Response
from sqlalchemy.orm import Session

from .. import schemas, database, oauth2 ,models

router = APIRouter(
    prefix="/vote",
    tags=["vote"]
)
@router.post("/" , status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Vote , db: Session = Depends(database.get_db) , current_user : int = Depends(oauth2.get_current_user) ):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id , models.User.id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} Voted already on this post with an id of: {vote.post_id}")
        new_vote = models.Vote(user_id = current_user.id ,post_id =  vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message" : "success on adding the vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote not found")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message" : "success on deleting the vote"}