import Tooltip from '@mui/material/Tooltip';
import { API_DOCS_URL, EMAIL } from '../config';
import '../styles/Header.css';

export const Header = () => {
  return (
    <header>
      <div className="header">
        <div className="header-brand">
          <div className="header-badge">VO</div>
          <div>
            <p className="header-kicker">Redis Product Search</p>
            <h2 className="header-title">Semantic catalog discovery</h2>
          </div>
        </div>
        <div className="cta-nav">
          <Tooltip title="Open the FastAPI documentation" arrow>
            <a href={API_DOCS_URL} className="header-link">
              API Docs
            </a>
          </Tooltip>
          <Tooltip title="Local project contact" arrow>
            <a className="header-cta" href={`mailto:${EMAIL}`}>
              Contact
            </a>
          </Tooltip>
        </div>
      </div>
    </header>
  );
};
