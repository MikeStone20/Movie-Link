/* eslint-disable no-undef */

const view = require('./view')
jest.mock('../jquery-3.5.1.min.js')
global.alert = jest.fn()

it('Add sessions valid', () => {
  global.alert.mockClear()
  // const $ = require('../jquery-3.5.1.min.js')
  // Call into the function we want to test
  document.body.innerHTML = '<h2 id = "mName">Shrek</h2>'
  document.body.innerHTML += '<form name="sessionsForm">'
  document.body.innerHTML += '<input type="text" id="zoom" name="zoom" value="link" >'
  document.body.innerHTML += '<input type="date" id="sessionDate" name="sessionDate" value="20201215">'
  document.body.innerHTML += '<input type="time" id="time" name="time" value="10:55">'
  document.body.innerHTML += '</form>'

  view.addSession()

  expect($.ajax).toBeCalledWith({
    type: 'POST',
    url: '/makeSession',
    dataType: 'json',
    contentType: 'application/json',
    data: '{"session":"Shrek,-10:55,link"}'
  })

  expect(global.alert).toHaveBeenCalledTimes(1)
})

it('Add sessions blank link', () => {
  global.alert.mockClear()
  // const $ = require('../jquery-3.5.1.min.js')
  // Call into the function we want to test
  document.body.innerHTML = '<h2 id = "mName">Shrek</h2>'
  document.body.innerHTML += '<form name="sessionsForm">'
  document.body.innerHTML += '<input type="text" value="" id="zoom" name="zoom">'
  document.body.innerHTML += '<input type="date" id="sessionDate" name="sessionDate" value="20201215">'
  document.body.innerHTML += '<input type="time" id="time" name="time" value="10:55">'
  document.body.innerHTML += '</form>'

  view.addSession()

  expect($.ajax).toBeCalledWith({
    type: 'POST',
    url: '/makeSession',
    dataType: 'json',
    contentType: 'application/json',
    data: '{"session":"Shrek,-10:55,"}'
  })

  expect(global.alert).toHaveBeenCalledTimes(1)
})

it('Add sessions blank movie', () => {
  global.alert.mockClear()
  // const $ = require('../jquery-3.5.1.min.js')
  // Call into the function we want to test
  document.body.innerHTML = '<h2 id = "mName"></h2>'
  document.body.innerHTML += '<form name="sessionsForm">'
  document.body.innerHTML += '<input type="text" id="zoom" name="zoom" value="link">'
  document.body.innerHTML += '<input type="date" id="sessionDate" name="sessionDate" value="20201215">'
  document.body.innerHTML += '<input type="time" id="time" name="time" value="10:55">'
  document.body.innerHTML += '</form>'

  view.addSession()

  expect($.ajax).toBeCalledWith({
    type: 'POST',
    url: '/makeSession',
    dataType: 'json',
    contentType: 'application/json',
    data: '{"session":",-10:55,link"}'
  })

  expect(global.alert).toHaveBeenCalledTimes(1)
})

it('Add wish list', () => {
  window.alert.mockClear()
  const $ = require('../jquery-3.5.1.min.js')
  // Call into the function we want to test
  document.body.innerHTML = '<h2 id = "mName">Matrix</h2>'

  view.addWishList()

  const movieIdStr = '{"movieName": "' + 'Matrix' + '"}'
  const jsonMovieID = JSON.parse(movieIdStr)

  expect($.ajax).toBeCalledWith({
    type: 'POST',
    url: '/addToWishlist',
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify(jsonMovieID)
  })

  expect(global.alert).toHaveBeenCalledTimes(1)
})

it('Add wish list no movie', () => {
  window.alert.mockClear()
  const $ = require('../jquery-3.5.1.min.js')
  // Call into the function we want to test
  document.body.innerHTML = '<h2 id = "mName"></h2>'

  view.addWishList()

  const movieIdStr = '{"movieName": "' + '' + '"}'
  const jsonMovieID = JSON.parse(movieIdStr)

  expect($.ajax).toBeCalledWith({
    type: 'POST',
    url: '/addToWishlist',
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify(jsonMovieID)
  })

  expect(global.alert).toHaveBeenCalledTimes(1)
})
