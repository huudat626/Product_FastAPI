import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Product } from './product';



@Injectable({
  providedIn: 'root'
})
export class ProductServiceService {

  // baseUrl = 'http://localhost:8080';
  product!: Product[];

  constructor(private http: HttpClient) { }

  getAll(): Observable<Product[]> {
    return this.http.get(`http://localhost:8080/product/`).pipe(
      map((res: any) => {
        if (!res) {
          throw new Error('Value expected!');
        } else {
          return res;
        }
      }),
      catchError((err) => {
        throw new Error(err.message);
      }));
  }
  create(product: any) {
    let params = new FormData();
    params.append("name" , product.name.toString());
    params.append("description",product.description.toString());
    params.append("price" , product.price.toString());

    console.log(params);
    return this.http.post(`http://localhost:8080/product/`, params).pipe(
      map((res: any) => {
        console.log(res);
        if (res.code == 1) {
          return res.data;
        }
        return null
      })
    );
  }
  update(product: any) {

    let params = new URLSearchParams();
    // params.append('_method', 'PUT')
    params.set("_id" , product._id.toString());
    params.set("name" , product.name.toString());
    params.set("description",product.description.toString());
    params.set("price" , product.price.toString());


    let options = {
      headers: new HttpHeaders().set('accept: application/json', 'Content-Type: application/json')
    }

    return this.http.put(`http://localhost:8080/product/${product._id}`, params.toString(),options).pipe(
      map((res: any)=>{
        return res;
      })
    );
  }
  delete(_id: string) {
    let params = new FormData();
    params.append("id" , _id);
    return this.http.delete(`http://localhost:8080/product/${_id}`).pipe(
      map((res: any)=>{
        // console.log(res);
        return res;
      })
    );
  }
}
