function handle_like(num){
    fetch(`/like/${num.post_id}`)
    .then(response => response.json())
    .then(result => {
          selected_post = document.getElementById(`${result.id}`);
          selected_post.querySelector(`.num-likes`).innerHTML = `${result.likes}`;
      });
}

function follow(){
    const postId = document.getElementById("profile_id").value;
    console.log(postId)

    fetch(`/follow/${postId}`, {method: 'GET'})
    .then(response => response.json())
    .then(result => {
          if(result.following){
            document.querySelector('.follow-btn').innerHTML = 'Following'
            document.querySelector('.follow-btn').id = 'following'
            document.querySelector('.followers_count').innerHTML  = `${result.followers}`
          }
          else{
            document.querySelector('.follow-btn').innerHTML = 'Follow +'
            document.querySelector('.follow-btn').id = 'not-following'
            document.querySelector('.followers_count').innerHTML  = `${result.followers}`

          }
      });
}