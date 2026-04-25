import { useEffect, useRef } from 'react';
import Chip from '@mui/material/Chip';
import Tooltip from '@mui/material/Tooltip';

import { TagRadios } from '../radio';
import { queryProducts, queryProductsWithLimit, resetPagination } from '../query';
import { Card } from './Card';

interface Props {
  products: any[];
  setProducts: (state: any) => void;
  gender: string;
  setGender: (state: any) => void;
  category: string;
  setCategory: (state: any) => void;
  total: number;
  setTotal: (state: any) => void;
}

export const Home = (props: Props) => {
  const initialProps = useRef(props);

  useEffect(() => {
    const currentProps = initialProps.current;

    resetPagination();
    currentProps.setGender('');
    currentProps.setCategory('');
    void queryProducts(currentProps, '', '');
  }, []);

  return (
    <main role="main" className="product-search-home">
      <section className="hero-panel">
        <div className="container hero-grid">
          <div>
            <p className="hero-eyebrow">Redis vector search demo</p>
            <h1 className="jumbotron-heading">Redis Product Search</h1>
            <p className="lead hero-copy">
              Explore a product catalog with semantic retrieval powered by Redis, FastAPI, and React.
              Browse inventory, filter by attributes, and find visually or textually similar products.
            </p>
          </div>
          <div className="hero-note">
            <p>Mode</p>
            <strong>Semantic Catalog</strong>
            <span>{props.total} indexed items ready for lookup</span>
          </div>
        </div>
        <div className="container control-row">
          {props.products && props.products.length > 0 ? (
            <TagRadios
              gender={props.gender}
              category={props.category}
              products={props.products}
              total={props.total}
              setGender={props.setGender}
              setCategory={props.setCategory}
              setProducts={props.setProducts}
              setTotal={props.setTotal}
            />
          ) : null}
          <Tooltip title="Load the next catalog slice" arrow>
            <button className="product-search-button" onClick={() => void queryProductsWithLimit(props)}>
              Load More
            </button>
          </Tooltip>
        </div>
      </section>
      <section className="album py-5 bg-light results-panel">
        <div className="container">
          <p className="catalog-count">
            <Tooltip title="Filtered item count" arrow>
              <em>{props.total} searchable items</em>
            </Tooltip>
          </p>
          <div>
            {props.category !== '' ? (
              <Chip
                style={{ margin: '5px 5px 25px 5px' }}
                label={`Category: ${props.category}`}
                variant='outlined'
                clickable
                color='primary'
                onDelete={() => {
                  resetPagination();
                  props.setCategory('');
                  void queryProducts(props, props.gender, '');
                }}
                disabled={props.category === ''}
              />
            ) : null}
            {props.gender !== '' ? (
              <Chip
                style={{ margin: '5px 5px 25px 5px' }}
                label={`Gender: ${props.gender}`}
                variant='outlined'
                clickable
                color='primary'
                onDelete={() => {
                  resetPagination();
                  props.setGender('');
                  void queryProducts(props, '', props.category);
                }}
                disabled={props.gender === ''}
              />
            ) : null}
          </div>
          {props.products && (
            <div className="row">
              {props.products.map((product) => (
                <Card
                  key={product.product_id}
                  imageUrl={product.img_url}
                  name={product.name}
                  productId={product.product_id}
                  numProducts={15}
                  similarityScore={product.similarity_score}
                  gender={props.gender}
                  category={props.category}
                  setProducts={props.setProducts}
                  setTotal={props.setTotal}
                />
              ))}
            </div>
          )}
        </div>
      </section>
    </main>
  );
};
