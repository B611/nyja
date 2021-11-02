import axios from "axios";

const API = axios.create({
  baseURL: process.env.REACT_APP_NYJA_API,
});

export const poll_status = (job_id) =>
  new Promise((resolve, reject) => {
    API.get("/status/" + job_id)
      .then((res) => {
        switch (res.data.status) {
          case "unknown":
            console.log("Unknown job id");
            break;
          case "finished":
            resolve(res.data.result);
            break;
          case "failed":
            console.log("failed", res);
            resolve(new Error("Job failed"));
            break;
          default:
            setTimeout(() => {
              resolve(poll_status(job_id));
            }, 500);
        }
      })
      .catch((err) => {
        // throw new Error(err);
      });
  });

export const run_task = (props) => {
  return API.post("/run_task", props)
    .then((res) => {
      const location = res.headers.location;
      const job_id = location.substring(location.lastIndexOf("/") + 1);
      return poll_status(job_id);
    })
    .catch((err) => {
      throw err;
    });
};

export const get_schedule = (props) => {
  return API.get("/schedule")
    .then((res) => {
      return res;
    })
    .catch((err) => {
      throw err;
    });
};

export const set_schedule = (props) => {
  return API.post("/schedule", props)
    .then((res) => {
      return res;
    })
    .catch((err) => {
      throw err;
    });
};

export default API;
