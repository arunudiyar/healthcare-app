import http from "k6/http";

export default function () {
  http.get("https://fwdjxgz257.execute-api.ap-south-1.amazonaws.com/prod/realtime-data?device_id=device001");
}
