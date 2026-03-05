module.exports = (req, res, next) => {
  if (req.path === '/400') {
    return res.status(400).json({
      error: "Bad Request (400)",
      message: "The data you sent is missing or malformed."
    });
  }

  if (req.path === '/401') {
    return res.status(401).json({
      error: "Unauthorized (401)",
      message: "You are not logged in or your token has expired."
    });
  }

  if (req.path === '/403') {
    return res.status(403).json({
      error: "Forbidden (403)",
      message: "You are logged in but do not have permission to perform this action."
    });
  }

  if (req.path === '/404') {
    return res.status(404).json({
      error: "Not Found (404)",
      message: "The requested path or resource does not exist."
    });
  }

  if (req.path === '/500') {
    return res.status(500).json({
      error: "Internal Server Error (500)",
      message: "The server encountered an issue while processing data. Please try again later."
    });
  }

  if (req.headers['force-error']) {
    const errorCode = parseInt(req.headers['force-error']) || 500;
    return res.status(errorCode).json({
      error: `Forced error with code ${errorCode} via Header!`
    });
  }

  next();
}
