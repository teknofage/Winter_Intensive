from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime

# fix
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Boycott_Inc')
client = MongoClient(host=host)
db = client.Boycott_Inc
boycotts_collection = db.boycotts
links_collection = db.links
comments_collection = db.comments

app = Flask(__name__, static_url_path='')

# fix
def link_url_creator(id_lst):
    links = []
    for link_id in id_lst:
        link = '' + link_id
        links.append(link)
    return links

@app.route('/')
def boycotts_index():
    """Show all boycotts."""
    return render_template('boycotts_index.html', boycotts=boycotts_collection.find())
    
    
@app.route('/boycotts/new')
def boycotts_new():
    """Create a new boycott."""
    return render_template('boycotts_new.html', boycott={}, title='New Boycott')


# Note the methods parameter that explicitly tells the route that this is a POST
@app.route('/boycotts', methods=['POST'])
def boycotts_submit():
    """Submit a new boycott."""
    # Grab the link IDs and make a list out of them
    link_ids = request.form.get('link_ids').split()
    # call our helper function to create the list of links
    links = link_url_creator(link_ids)
    boycott = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        # 'time_frame': time_frame,
        'links': links,
        'comments': request.form.get('comments')
    }
    boycott_id = boycotts_collection.insert_one(boycott).inserted_id
    return redirect(url_for('boycotts_show', boycott_id=boycott_id))

@app.route('/boycotts/<boycott_id>', methods= ['GET'])
def boycotts_show(boycott_id):
    """Show a single boycott."""
    boycott = boycotts_collection.find_one({"_id": ObjectId(boycott_id)})
    comments = comments_collection.find({"_id": ObjectId(boycott_id)})
    return render_template('boycotts_show.html', boycott=boycott, comments=comments)

@app.route('/boycotts/<boycott_id>/edit')
def boycotts_edit(boycott_id):
    """Show the edit form for a boycott."""
    # Add the title parameter here
    boycott = boycotts_collection.find_one({"_id": ObjectId(boycott_id)})
    return render_template('boycotts_edit.html', boycott=boycott, title="Edit Boycott")

@app.route('/boycotts/<boycott_id>', methods=['POST'])
def boycotts_update(boycott_id):
    """Submit an edited boycott."""
    link_ids = request.form.get('link_ids').split()
    links = link_url_creator(link_ids)
    # create our updated boycott
    updated_boycott = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'links': links,
        'link_ids': link_ids,
        'comments': request.form.get('comments')
    }
    # set the former boycott to the new one we just updated/edited
    boycotts_collection.update_one(
        {'_id': ObjectId(boycott_id)},
        {'$set': updated_boycott})
    # take us back to the boycott's show page
    return redirect(url_for('boycotts_show', boycott_id=boycott_id))

@app.route('/boycotts/<boycott_id>/delete', methods=['POST'])
def boycotts_delete(boycott_id):
    """Delete one boycott."""
    boycotts_collection.delete_one({'_id': ObjectId(boycott_id)})
    return redirect(url_for("boycotts_index"))

# Add this header to distinguish Comment routes from Boycott routes
########## COMMENT ROUTES ##########    

@app.route('/boycotts/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    # TODO: Fill in the code here to build the comment object,
    # and then insert it into the MongoDB comments collection
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'boycott_id': ObjectId(request.form.get('boycott_id')),
        'created_at': datetime.now()
    }

    print(comment)
    comment_id = comments_collection.insert_one(comment).inserted_id
    return redirect(url_for('boycotts_show', boycott_id=request.form.get('boycott_id')))

@app.route('/boycotts/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments_collection.find_one({'_id': ObjectId(comment_id)})
    comments_collection.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('boycotts_show', boycott_id=comment.get('boycott_id')))    


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
