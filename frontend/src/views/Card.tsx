import Chip from '@mui/material/Chip';
import Tooltip from '@mui/material/Tooltip';

import { getSemanticallySimilarProducts, getVisuallySimilarProducts } from '../api';
import useCheckMobileScreen from '../mobile';

interface Props {
  productId: number;
  numProducts: number;
  imageUrl: string;
  name: string;
  gender: string;
  category: string;
  similarityScore: number;
  setProducts: (state: any) => void;
  setTotal: (state: any) => void;
}

export const Card = (props: Props) => {
  const isMobile = useCheckMobileScreen();

  const queryVisuallySimilarProducts = async () => {
    try {
      const res = await getVisuallySimilarProducts(props.productId, 'KNN', props.gender, props.category, props.numProducts);
      props.setProducts(res.items);
      props.setTotal(res.total);
    } catch (err) {
      console.log(String(err));
    }
  };

  const querySemanticallySimilarProducts = async () => {
    try {
      const res = await getSemanticallySimilarProducts(props.productId, 'KNN', props.gender, props.category, props.numProducts);
      props.setProducts(res.items);
      props.setTotal(res.total);
    } catch (err) {
      console.log(String(err));
    }
  };

  const getCardSize = () => (isMobile ? '50%' : '20%');

  return (
    <div className="col-md-2" style={{ width: getCardSize() }}>
      <div className="card mb-3 box-shadow vector-card">
        <img className="card-img-top vector-card-image" src={props.imageUrl} alt={props.name} />
        <div className="card-body">
          <p className="card-text vector-card-title">{props.name}</p>
          <div style={{ alignContent: 'left' }}>
            <b>Related Views</b>
          </div>
          <div className="d-flex justify-content-between align-items-center gap-2">
            <div className="btn-group">
              <Tooltip title="Search for semantically similar products" arrow>
                <button type="button" className="btn btn-sm btn-outline-secondary" onClick={() => void querySemanticallySimilarProducts()} style={{ fontSize: 12 }}>
                  By Meaning
                </button>
              </Tooltip>
              <Tooltip title="Search for visually similar products" arrow>
                <button type="button" className="btn btn-sm btn-outline-secondary" onClick={() => void queryVisuallySimilarProducts()} style={{ fontSize: 12 }}>
                  By Image
                </button>
              </Tooltip>
            </div>
            <div className="btn-group">
              {props.similarityScore ? (
                <Tooltip title="Similarity score" arrow>
                  <Chip style={{ margin: 'auto', fontSize: 12 }} label={props.similarityScore.toFixed(2)} color='primary' />
                </Tooltip>
              ) : null}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
