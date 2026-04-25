import { FC } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Layout from './Layout';
import { API_DOCS_URL } from './config';

const DocsRedirect: FC = () => {
  window.location.replace(API_DOCS_URL);
  return null;
};

export const AppRoutes: FC = () => {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />} />
        <Route path="/api/docs" element={<DocsRedirect />} />
      </Routes>
    </Router>
  );
};
