/* eslint-disable no-undef */

const userHome = require('./sessions')
jest.mock('../jquery-3.5.1.min.js')

test('Blank movie search test', () => {
  const t = '<input type="text" placeholder="Movie Search" id="clientBox"/>'
  document.body.innerHTML = t
  document.body.innerHTML += '<a class="nav-link" id="movie_search" onclick="movieSearch()" href="">Movie Search</a>'

  userHome.movieSearch()

  expect((document.getElementById('movie_search')).getAttribute('href')).toBe('/movie_search/')
})

test('Movie search test with movie', () => {
  const t = '<input type="text" placeholder="Movie Search" id="clientBox" value="Matrix"/>'
  document.body.innerHTML = t
  document.body.innerHTML += '<a class="nav-link" id="movie_search" onclick="movieSearch()" href="">Movie Search</a>'

  userHome.movieSearch()

  expect((document.getElementById('movie_search')).getAttribute('href')).toBe('/movie_search/Matrix')
})

test('Blank friend search test', () => {
  const t = '<input type="text" placeholder="Friend Search" id="clientBox2" />'
  document.body.innerHTML = t
  document.body.innerHTML += '<a class="nav-link" id="friend_search" onclick="friendSearch()" href="">Friend Search</a>'

  userHome.friendSearch()

  expect((document.getElementById('friend_search')).getAttribute('href')).toBe('/searchUser/')
})

test('Friend search test with friend', () => {
  const t = '<input type="text" placeholder="Friend Search" id="clientBox2" value="Mike"/>'
  document.body.innerHTML = t
  document.body.innerHTML += '<a class="nav-link" id="friend_search" onclick="friendSearch()" href="">Friend Search</a>'

  userHome.friendSearch()

  expect((document.getElementById('friend_search')).getAttribute('href')).toBe('/searchUser/Mike')
})

test('Quick add test', () => {
  // var wishList = document.getElementById('myMovies')
  document.body.innerHTML = '<div id="myMovies">' + '</div>'

  userHome.quickAdd('Jumanji')

  let temp = '<div id="myMovies">' + '<ul><li>' + 'Jumanji'
  temp += '</li></ul>' + '</div>'

  expect(document.body.innerHTML).toBe(temp)
})

it('Quick add ajax test', () => {
  const $ = require('../jquery-3.5.1.min.js')
  // Call into the function we want to test
  document.body.innerHTML = '<div id="myMovies">' + '</div>'

  userHome.quickAdd('Jumanji')

  const movieIdStr = '{"movieName": "' + 'Jumanji' + '"}'
  const jsonMovieID = JSON.parse(movieIdStr)

  expect($.ajax).toBeCalledWith({
    type: 'POST',
    url: '/addToWishlist',
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify(jsonMovieID)
  })
})

it('Refresh top test', () => {
  const $ = require('../jquery-3.5.1.min.js')
  // Call into the function we want to test
  userHome.refreshTopMovies()

  expect($.ajax).toBeCalledWith({
    type: 'GET',
    url: '/getPopular',
    dataType: 'json',
    contentType: 'application/json',
    data: { data: 'check' },
    success: expect.any(Function),
    error: expect.any(Function)
  })
})

test('Update HTML test valid', () => {
  // var wishList = document.getElementById('myMovies')
  document.body.innerHTML = '<div id="popularMovies">' + '</div>'

  const data = 'Shrek,Shrek 2'
  userHome.updateHTML(data)

  let temp = '<div id="popularMovies">'

  temp += '<br> Top Movies (Click to add to Wish List):'
  temp += '<ul></ul>'
  let temp2 = '<li><button type="button" id="quickAdd" onclick="quickAdd(\''
  temp2 += 'Shrek'
  temp2 += '\')">'
  temp2 += 'Shrek'
  temp2 += '</button></li>'
  temp += temp2

  let temp3 = '<li><button type="button" id="quickAdd" onclick="quickAdd(\''
  temp3 += 'Shrek 2'
  temp3 += '\')">'
  temp3 += 'Shrek 2'
  temp3 += '</button></li>'
  temp += temp3

  temp += '</div>'

  expect(document.body.innerHTML).toBe(temp)
})

test('Update HTML test invalid', () => {
  // var wishList = document.getElementById('myMovies')
  document.body.innerHTML = '<div id="popularMovies">' + '</div>'

  const data = ''
  userHome.updateHTML(data)

  let temp = '<div id="popularMovies">'

  temp += '<br> Top Movies (Click to add to Wish List):'
  temp += '<ul></ul>'
  let temp2 = '<li><button type="button" id="quickAdd" onclick="quickAdd(\''
  temp2 += 'IMDb failure'
  temp2 += '\')">'
  temp2 += 'IMDb failure'
  temp2 += '</button></li>'
  temp += temp2

  temp += '</div>'

  expect(document.body.innerHTML).toBe(temp)
})
