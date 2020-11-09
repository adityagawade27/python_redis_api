# API implementation for storing a list of my favorite books and their details to mark books read / unread 

## Usage 

All responses will have the following form: 
```json
{
    "data": "Mixed data type that holds the response content",
    "message": "Description of Response and it's status"
}
```

##  
`GET /book_list` --> 200 Response OK 
Key --> book_id --> six digit hex 
Return 
```json
[
    {
        "ABC123": {
            "book_title": "The Hard Way",
            "author" : "Lee Child",
            "release_year": "2006",
            "genre": "Thriller",
            "read": true,
            "page_nos": 455,
            "rating":"Great"
        }
    },
    {
        "DEF456": {
            "book_title": "The Innocent",
            "author" : "David Baldacci",
            "release_year": "2012",
            "genre": "Thriller",
            "read": false,
            "page_nos": 375,
            "rating": null
        }
    }
]

Add a book to the list 

`POST /book_list` 

 **Arguments**
-  "book_title"
-  "author"
-  "release_year"
-  "genre"
-  "read"
-  "page_nos"

**Response**
- `201 Created` on success 
```json
{
    "ABC123": {
        "book_title": "The Hard Way",
        "author" : "Lee Child",
        "release_year": "2006",
        "genre": "Thriller",
        "read": true,
        "page_nos": 455,
        "rating": "Fine"
    }
}```

# Lookup book details 
`GET /book_list/<book_id>`

**Response**
- 404 Not Found
- 200 OK on success

** Update book status 

`PUT /book_list/<book_id>`

**Arguments**
```json
{
    "read": true
}```

** Reponse ** 

- `204 OK` response updated 
- `404 Not Found`


