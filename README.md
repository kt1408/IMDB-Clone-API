# IMDB-Clone-API
IMDB Clone REST API is build using Django REST Framework


It's a REST API which is a clone of IMDB API, build using Django REST Framework and it has different functions like:
* Stream Platform Can be Added
* In WatchList movies,tv shows,web series etc. can be added
* Evey item in WatchList has average rating and number of reviews it has
* Reviews can be added for any item and can be updated also
* Review List can be viewed and individual review can also be viewed for a
particular user or watchList item also.
* Stream Platform & WatchList can be added by admin only
* Reviews can be added by any user but be updated or deleted by only the user who has 
created that review or by admin.

During this project used different functions of DRF such as **Serializers, Function-BasedViews, Class-Based Views, Viewsets and Routers, Permissions, Authentications, Throttling, Django Filter Backend, Pagination, Automated API Testing**

## URLs to access differnt pages are

1. Admin Access

    Admin Section: http://127.0.0.1:8000/admin/


2. Accounts

    Registration: http://127.0.0.1:8000/account/register/
    Login: http://127.0.0.1:8000/account/login/
    Logout: http://127.0.0.1:8000/account/logout/


3. Stream Platforms

    Create Element & Access List: http://127.0.0.1:8000/watch/stream/
    Access, Update & Destroy Individual Element: http://127.0.0.1:8000/watch/stream/<int:streamplatform_id>/


4. Watch List

    Create & Access List: http://127.0.0.1:8000/watch/list/
    Access, Update & Destroy Individual Element: http://127.0.0.1:8000/watch/<int:movie_id>/


5. Reviews

    Create Review For Specific Movie: http://127.0.0.1:8000/watch/<int:movie_id>/review/create/
    List Of All Reviews For Specific Movie: http://127.0.0.1:8000/watch/<int:movie_id>/review/
    Access, Update & Destroy Individual Review: http://127.0.0.1:8000/watch/review/<int:review_id>/


6. User Review

    Access All Reviews For Specific User: http://127.0.0.1:8000/watch/user-reviews/?username=example

