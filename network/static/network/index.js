if(!localStorage.getItem('starting')){
    localStorage.setItem('starting',0)
}
// Load posts 10 at a time
const quantity = 11;

document.addEventListener('DOMContentLoaded', load);

function load() {
    document.querySelector('.next-btn').style.display = 'none';
    document.querySelector('.previous-btn').style.display = 'none';

    // Set start and end post numbers, and update counter
    const start = localStorage.getItem('starting');
    const end = start*1 + quantity - 1;
    starting = end + 1;
    console.log(end)

    document.getElementById("posts").innerHTML='';
    // Get new posts and add posts
    fetch(`/posts?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data => {
        data.forEach(show_post);
        if(data.length >= 10 && start==0){
            document.querySelector('.next-btn').style.display = 'block';
        }
        if(data.length >= 10 && start > 0){
            document.querySelector('.previous-btn').style.display = 'block';
            document.querySelector('.next-btn').style.display = 'block';
        }
        if(data.length <= 10 && start > 0){
            document.querySelector('.previous-btn').style.display = 'block';
        }
    })
};

function handle_like(post){
    fetch(`/like/${post.id}`)
    .then(response => response.json())
    .then(result => {
          selected_post = document.getElementById(`${post.id}`);
          selected_post.querySelector(`.num-likes`).innerHTML = `${result.likes}`;
      });
}

//saving edit
function save_edit(post){
    fetch(`/save/${post.id}`, {
        method: 'POST',
        body: JSON.stringify({
            content: document.querySelector('.edit-content').value
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
          load();
      });
    }


//edit content
function edit_post(post){
    //create text are and button
    selected_post = document.getElementById(`${post.id}`);
    edit_text = document.createElement('textarea');
    submit_edit = document.createElement('button');
    edit_text.value = `${post.content}`;
    submit_edit.innerHTML = 'Save';
    submit_edit.className = 'edit-btn';
    edit_text.className = 'edit-content';

    submit_edit.onclick = function(){
        save_edit(post);};

    current_text = selected_post.querySelector('.postedContent');

    button_box = selected_post.querySelector('.button_item');
    data_box = selected_post.querySelector('.post_data');

    data_box.append(edit_text);
    button_box.append(submit_edit);

    current_text.style.display = 'none';
    selected_post.querySelector('.edit-btn').style.display = 'none';
}

function show_post(post) {
    // // Create new post
    const item1 = document.createElement("div");
    const item2 = document.createElement("div");
    const item3 = document.createElement("div");
    item1.className = 'post_item';
    item2.className = 'post_data';
    item3.className = 'like_item';

    const box = document.createElement("div");
    box.className = 'section'

    const title = document.createElement("a");
    const timestamp = document.createElement("p");
    const content = document.createElement("h6");
    const like = document.createElement("button");
    const num_likes = document.createElement("h7");
    like.className = 'like-btn'
    num_likes.className = 'num-likes'
    num_likes.id = `${post.id}`;

    like.innerHTML = `Like`;
    like.onclick = function(){
    handle_like(post);};
    num_likes.innerHTML = `${post.likes}`;
    content.innerHTML = `${post.content}`;
    content.className = 'postedContent'
    content.disabled = true;
    title.innerHTML = `${post.creator}`;
    title.href = `/profile/${post.creator_id}`;
    timestamp.innerHTML = `Posted on ${post.timestamp}`;
    
    document.getElementById("posts").appendChild(box);
    item1.append(title);
    box.appendChild(item1);
    item2.append(content);
    item2.append(timestamp);
    box.appendChild(item2);
    item3.append(num_likes);
    item3.append(like);
    box.appendChild(item3);
    box.id = `${post.id}`;

    // edit button 
    if(post.editable){
        const item4 = document.createElement("div");
        item4.className = 'button_item';
        const edit = document.createElement("button");
        edit.innerHTML = 'Edit';
        edit.className = 'edit-btn';
        edit.onclick = function(){
            edit_post(post);};
        item4.append(edit);
        box.appendChild(item4);
    }

};

function next_post(){
    start = localStorage.getItem('starting');
    localStorage.setItem('starting',start*1+10)
    localStorage.setItem('starting',start*1+10);
    load();
}


function back_post(){
    start = localStorage.getItem('starting');
    localStorage.setItem('starting',start*1-10)
    localStorage.setItem('starting',start*1-10);
    load();
}