import request from 'superagent';

export const requester = {
  get: (path, data, params = []) => {
    // path and headers
    const req = request
      .get(`/api/${path}`)
      .set('Content-Type', 'application/json');
    // query params
    params.map((x) => req.query(x));
    // data
    req.send(JSON.stringify(data));
    return req;
  },
  post: (path, data) => request
    .post(`/api/${path}`)
    .set('Content-Type', 'application/json')
    .send(JSON.stringify(data)),
  postImage: (path, image_black) => request
    .post(`/api/${path}`)
    .attach('image_black', image_black),
  put: (path, data) => request
    .put(`/api/${path}`)
    .set('Content-Type', 'application/json')
    .send(JSON.stringify(data)),
  delete: (path, data) => request
    .delete(`/api/${path}`)
    .set('Content-Type', 'application/json')
    .send(JSON.stringify(data))
};
