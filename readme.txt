## To activate virtual environment
source bin/Activate

## To run Paste server
sudo python3 -m bottle --server paste --bind 127.0.0.1:80 --debug --reload app

## Stop the server
Control + C

## run tailwindcss
(Be in tailwindcss folder first)
npx tailwindcss -i input.css -o ../app.css --watch

#########################
ROUTES/ROUTING

C - Create (Post)
R - Read (Get)
U - Update (Put / Patch)
D - Delete (Delete)


/items                    GET - To get many items
/items/1                  GET - To get one item
/items                    POST - Create or save an item
/items/1                  DELETE - To delete an item
/items/1                  PUT or PATCH - To update the item