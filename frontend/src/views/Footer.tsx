import { EMAIL } from '../config';
import '../styles/Footer.css';

export const Footer = () => {
  return (
    <footer>
      <div className='footer'>
        <div>Redis Product Search is a local demo for vector-based product discovery.</div>
        <div>
          <a href='/api/docs'>Backend API</a>
          <span> | </span>
          <a href='https://fastapi.tiangolo.com/'>FastAPI</a>
          <span> | </span>
          <a href='https://react.dev/'>React</a>
        </div>
        <div>contact: {EMAIL}</div>
      </div>
    </footer>
  );
};
