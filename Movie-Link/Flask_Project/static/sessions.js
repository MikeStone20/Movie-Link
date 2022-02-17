/* global $ */
window.$ = require('../jquery-3.5.1.min.js')

function movieSearch () { // eslint-disable-line no-unused-vars
  let value = '/movie_search/'
  value += document.getElementById('clientBox').value
  document.getElementById('movie_search').setAttribute('href', value)
}

function friendSearch () { // eslint-disable-line no-unused-vars
  let value2 = '/searchUser/'
  value2 += document.getElementById('clientBox2').value
  document.getElementById('friend_search').setAttribute('href', value2)
}

function quickAdd (movieName) { // eslint-disable-line no-unused-vars
  console.log('Quick adding')
  const div = document.getElementById('myMovies')

  const temp = '<ul>' + '<li>' + movieName + '</li>'
  div.innerHTML += temp

  const movieIdStr = '{"movieName": "' + movieName + '"}'
  const jsonMovieID = JSON.parse(movieIdStr)

  return $.ajax({
    type: 'POST',
    url: '/addToWishlist',
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify(jsonMovieID) // "{"movie": "name"}"
  })
}

function refreshTopMovies () { // eslint-disable-line no-unused-vars
  return $.ajax({
    type: 'GET',
    url: '/getPopular',
    dataType: 'json',
    contentType: 'application/json',
    data: { data: 'check' },
    success: function (data) { updateHTML(data) },
    error: function (data) { console.log('Error') }
  })
}

function updateHTML (data) {
  const div = document.getElementById('popularMovies')
  let newList = ['IMDb failure']
  if (data.indexOf(',') !== -1) {
    newList = data.split(',')
  }
  let temp = 'temp'
  div.innerHTML = '<br> Top Movies (Click to add to Wish List):<ul>'
  for (let i = 0; i < newList.length; i++) {
    temp = '<li><button type=\'button\' id=\'quickAdd\' onclick="quickAdd(\''
    temp += newList[i]
    temp += '\')">'
    temp += newList[i]
    temp += '</button></li>'
    div.innerHTML += temp
  }
  div.innerHTML += '</ul>'
}

module.exports = {
  quickAdd,
  refreshTopMovies,
  movieSearch,
  friendSearch,
  updateHTML
}
