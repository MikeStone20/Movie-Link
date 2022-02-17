/* eslint-disable no-undef */

const friend = require('./friendSearch')
jest.mock('../jquery-3.5.1.min.js')
window.alert = jest.fn()

it('Friend 1 add test', () => {
  window.alert.mockClear()
  const $ = require('../jquery-3.5.1.min.js')
  // Call into the function we want to test
  document.body.innerHTML = '<h6 id = "friend1">Mike</h6>'
  document.body.innerHTML += '<h6 id = "email1">mike@gmail.com</h6>'

  friend.addFriend('1')

  const friendInfoStr = '{"name": "' + 'Mike' + '", "email": "' + 'mike@gmail.com' + '"}'
  const friendInfoJSON = JSON.parse(friendInfoStr)

  expect($.ajax).toBeCalledWith({
    type: 'POST',
    url: '/addFriend',
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify(friendInfoJSON)
  })
})

it('Friend 5 add test ', () => {
  window.alert.mockClear()
  const $ = require('../jquery-3.5.1.min.js')
  // Call into the function we want to test
  document.body.innerHTML = '<h6 id = "friend5">Debby</h6>'
  document.body.innerHTML += '<h6 id = "email5">Debby@gmail.com</h6>'

  friend.addFriend('5')

  const friendInfoStr = '{"name": "' + 'Debby' + '", "email": "' + 'Debby@gmail.com' + '"}'
  const friendInfoJSON = JSON.parse(friendInfoStr)

  expect($.ajax).toBeCalledWith({
    type: 'POST',
    url: '/addFriend',
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify(friendInfoJSON)
  })
})
