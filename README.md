# ROUTES:
 

 `GET /` - home route (health check) -- 200 OK
 `GET /posts` - returns all posts
 `POST /create-post` - allows to create a post and returns its id
 
 `GET /posts/{id}` - returns one post with matching id
 `PATCH /posts/{id}` - update `title` or `body` of the post matching the id
 `DELETE /posts/{id}` - delete post matching the id
 