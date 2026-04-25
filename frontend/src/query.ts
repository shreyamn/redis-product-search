import { getCatalogItems } from './api';

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

let skip = 0;
const limit = 15;

export const resetPagination = () => {
  skip = 0;
};

export const queryProducts = async (props: Props, gender: string, category: string) => {
  try {
    const result = await getCatalogItems(limit, skip, gender, category);
    props.setProducts(result.items);
    props.setTotal(result.total);
  } catch (err) {
    console.log(err);
  }
};

export const queryProductsWithLimit = async (props: Props) => {
  try {
    skip += limit;
    const result = await getCatalogItems(limit, skip, props.gender, props.category);
    props.setProducts([...props.products, ...result.items]);
    props.setTotal(result.total);
  } catch (err) {
    console.log(err);
  }
};
