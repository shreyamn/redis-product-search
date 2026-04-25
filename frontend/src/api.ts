import { MASTER_URL } from './config';

export const fetchFromBackend = async (url: string, method: string, body?: unknown) => {
  const request = new Request(url, {
    method,
    body: body ? JSON.stringify(body) : undefined,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });

  const response = await fetch(request);

  if (response.status === 500) {
    throw new Error('Internal server error');
  }

  if (response.status === 401 || response.status === 403) {
    window.location.href = '/';
  }

  const data = await response.json();

  if (response.status > 400 && response.status < 500) {
    if (data.detail) {
      throw data.detail;
    }
    throw data;
  }

  return data;
};

export const getCatalogItems = async (limit = 15, skip = 0, gender = '', category = '') => {
  const params = new URLSearchParams({
    limit: String(limit),
    skip: String(skip),
  });

  if (gender) {
    params.set('gender', gender);
  }

  if (category) {
    params.set('category', category);
  }

  return fetchFromBackend(`${MASTER_URL}?${params.toString()}`, 'GET');
};

export const getVisuallySimilarProducts = async (
  id: number,
  search = 'KNN',
  gender = '',
  category = '',
  limit = 15,
) => {
  const body = {
    product_id: id,
    search_type: search,
    gender,
    category,
    number_of_results: limit,
  };

  return fetchFromBackend(`${MASTER_URL}vectorsearch/image`, 'POST', body);
};

export const getSemanticallySimilarProducts = async (
  id: number,
  search = 'KNN',
  gender = '',
  category = '',
  limit = 15,
) => {
  const body = {
    product_id: id,
    search_type: search,
    gender,
    category,
    number_of_results: limit,
  };

  return fetchFromBackend(`${MASTER_URL}vectorsearch/text`, 'POST', body);
};
