/* global $ */
window.$ = require('../jquery-3.5.1.min.js')
window.alert = require('../jquery-3.5.1.min.js')

function addFriend (fNum) { // eslint-disable-line no-unused-vars
  fNum = fNum.toString()
  const friendName = document.getElementById('friend' + fNum).innerHTML
  const fEmail = document.getElementById('email' + fNum).innerHTML

  const friendInfoStr = '{"name": "' + friendName + '", "email": "' + fEmail + '"}'

  console.log(friendInfoStr)
  const friendInfoJSON = JSON.parse(friendInfoStr)

  $.ajax({
    type: 'POST',
    url: '/addFriend',
    dataType: 'json',
    contentType: 'application/json',
    // "{"name": "usr_name", "email" : "fEmail" }"
    data: JSON.stringify(friendInfoJSON)
  })

  window.alert('Friend added')
}

module.exports = {
  addFriend
}
