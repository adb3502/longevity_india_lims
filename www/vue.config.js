module.exports = {
  devServer: {
    // It tells the frontend dev server (which will run on port 8080)
    // to forward any API requests it doesn't recognize to our backend Tomcat server
    // running on port 8082.
    proxy: 'http://localhost:8082'
  }
}