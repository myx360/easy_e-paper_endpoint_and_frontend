import { requester as reqr } from './http';
import { from } from 'rxjs';

export const requester = {
  get: (path, data, params) => from(reqr.get(path, data, params)),
  post: (path, data) => from(reqr.post(path, data)),
  postImage: (path, file) => from(reqr.postImage(path, file)),
  put: (path, data) => from(reqr.put(path, data)),
  delete: (path, data) => from(reqr.delete(path, data))
}