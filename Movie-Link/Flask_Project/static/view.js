/* global $ */
window.$ = require('../jquery-3.5.1.min.js')
function addWishList () { // eslint-disable-line no-unused-vars
  const movieName = document.getElementById('mName').innerHTML
  const movieIdStr = '{"movieName": "' + movieName + '"}'
  const jsonMovieID = JSON.parse(movieIdStr)

  window.alert('Added to wish list')
  return $.ajax({
    type: 'POST',
    url: '/addToWishlist',
    dataType: 'json',
    contentType: 'application/json', // "{"movie": "name"}"
    data: JSON.stringify(jsonMovieID)
  })
}

function addSession () { // eslint-disable-line no-unused-vars
  const comma = ','
  const dash = '-'

  const movieName = document.getElementById('mName').innerHTML
  const zoomLink = comma.concat(document.getElementById('zoom').value)
  let seshDate = comma.concat(document.getElementById('sessionDate').value)
  seshDate = seshDate.replace(/[./#!$%^&*;:{}=\-_`~()]/g, '')
  const seshTime = dash.concat(document.getElementById('time').value)

  let seshStr = movieName.concat(seshDate, seshTime, zoomLink)

  console.log(seshStr)
  // example {session: "movieName1,03282020-10:30-PM,link"}
  seshStr = '{"session": "' + seshStr + '"}'
  const jsonSession = JSON.parse(seshStr)
  window.alert('Added to sessions')
  return $.ajax({
    type: 'POST',
    url: '/makeSession',
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify(jsonSession) // "{"movie": "name"}"
  })
}

module.exports = {
  addSession,
  addWishList
}
