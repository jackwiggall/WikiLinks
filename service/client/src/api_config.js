var API_HOST = 'http://141.98.252.168:55533/'
if (process.env.NODE_ENV === 'development') {
  API_HOST = 'http://localhost:3000/'
}
module.exports = {
  API_HOST: API_HOST,
  API_LINK_PAGES_DEV: API_HOST+'api/v1/devLinkPages',
  API_LINK_PAGES: API_HOST+'api/v1/linkPages'
}