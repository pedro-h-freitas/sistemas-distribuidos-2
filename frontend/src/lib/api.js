class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function apiFetch(
  path,
  options = {},
){
  const {
    method = "GET",
    body,
  } = options;

  const requestHeaders = new Headers();

  requestHeaders.set("Accept", "application/json");

  if (body !== undefined) {
    requestHeaders.set("Content-Type", "application/json");
  }

  const response = await fetch(path, {
    method,
    headers: requestHeaders,
    body: body === undefined ? undefined : JSON.stringify(body),
    cache: "no-store",
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => null);

    const detail =
      typeof errorBody?.detail === "string"
        ? errorBody.detail
        : `Falha na requisição (${response.status}).`;

    throw new ApiError(response.status, detail);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}


export async function apiGet(path) {
  return apiFetch(path)
}


export async function apiPost(path, body) {
  return apiFetch(path, { method: 'POST', body })
}


export async function apiPatch(path, body) {
  return apiFetch(path, { method: 'PATCH', body })
}


export async function apiPut(path, body) {
  return apiFetch(path, { method: 'PUT', body })
}


export async function apiDelete(path) {
  return apiFetch(path, { method: 'DELETE' })
}

