import axios from "axios";
import { buildHeaders } from "../helpers/AppHelper";

export const request = async (method, path, data, params) =>
  (
    await axios({
      method,
      url: `${API_BASE_URL}${path}`,
      data,
      params,
      headers: buildHeaders(),
    })
  ).data;
export const allCategories = async () => {
  const records = [];
  let page = 1;
  while (page) {
    const result = await request("get", "/categories", undefined, {
      page,
      per_page: 100,
    });
    records.push(...result.records);
    page = result.next_page;
  }
  return records;
};
