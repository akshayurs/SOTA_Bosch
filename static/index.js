console.log('Started')
var url = 'http://localhost:5000'
var socket = io.connect(url)
var users = {}
var software
var signature
var testersid
var testerpublickey
var mysignature

function loader(state,text) {
  console.log("loader",state,text);
  document.querySelector('.loader').style.display = state == true ? 'flex' : 'none'
  document.querySelector('#loader-text').innerHTML = text
}

const form1 = document.querySelector('.form1')
form1.addEventListener('submit', (e) => {
  e.preventDefault()
  const formdata = new FormData(form1)
  type = formdata.get('type')
  name = formdata.get('name')
  if(type=='Car'){
    document.querySelector('.to-tester').style.display = "none"
  }else{
    document.querySelector('.to-car').style.display = "none"
  }
  document.querySelectorAll(".hide").forEach(ele=>ele.classList.remove("hide"))
  loader(true,"Generating keys")
  socket.emit('new_key_req', { name: name, type: type })
})

function send_soft_js(software, signature){
  let tosid = Object.keys(users).filter((key) => users[key]['type'] == 'Car')
  if (!tosid) {
    return alert('No car connected')
  }
  loader(true, 'Sending software')
  setTimeout(() => loader(false), 1000)
  socket.emit('software_update', { software: software, sid: tosid, signature })
  console.log(software, signature, tosid)
}



disconnect = async () => {
  await fetch(url + '/disconnect/' + sid)
  window.location.reload()
}

socket.on('connect', function () {
  socket.on('new_key_res', (data) => {
    console.log(data)
    my_public_key = data.public_key
    my_private_key = data.private_key
    sid = data.sid
    document.querySelector(".my-sid").value = sid
    document.querySelector('.my-public-key').value = my_public_key
    document.querySelector('.my-private-key').value = my_private_key
    loader(false)
  })
  socket.on('new_user_keys', (data) => {
    console.log(data)
    if (!data || Object.keys(data).length==0) return
    let list = document.querySelector('.public-key-list')
    list.innerHTML = Object.keys(data)
      .map(
        (key, ind) =>
          `<tr><td>${data[key]['type']}</td><td>${data[key]['name']}</td><td><textarea id="user-${ind}">${data[key]['public_key']}</textarea></td></tr>`
      )
      .join('')
    users = data
  })
  socket.on('software_update', (data) => {
    loader(true,"Receiving software")
    setTimeout(()=>loader(false),1000)
    document.querySelector('#encrypted-data').value = data.encrypt_soft
    document.querySelector('#signature').value = data.signature
    testersid = data.testersid
    testerpublickey = users[testersid]['public_key']
    signature = data.signature
    console.log(data);
  })
})
