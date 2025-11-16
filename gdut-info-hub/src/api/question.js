import request from "../utils/request";

export function getAnswer(params) {
  return request({
    url: "/question",
    method: "get",
    params,
  });
}
