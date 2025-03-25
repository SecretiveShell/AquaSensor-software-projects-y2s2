async function _isLogged() {
  let tok = window.sessionStorage["AquaSensorToken"];
  return await fetch("/api/v1/auth/me", {
    headers: {
      Accept: "application/json",
      "AquaSensor-Login-Token": tok,
    },
  })
    .then((response) => response.json()
    .then((response) => {
      return "email" in response;
    }));
}

