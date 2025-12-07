import { fetch } from "../sanity";

export default async function() {
  const query = `*[_type == "student"]{
    name,
    email,
    linkedin,
    github,
    calendly,
    status
  }`;
  return await fetch(query);
};