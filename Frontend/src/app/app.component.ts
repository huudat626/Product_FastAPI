import { Component } from '@angular/core';
import { Product } from './product';
import { ProductServiceService } from './product-service.service';
import { mergeMap, tap } from 'rxjs/operators';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Frontend';
  error = '';
  success = '';
  flagSelected = false;
  public show: boolean = false;
  products!: Product[];
  selectedProduct: Product = {
    _id: null, name: null, price: null, description: null,
  }
  constructor(private apiService: ProductServiceService) {
  }
  ngOnInit(): void {
    this.getAll();
    this.flagSelected = false;
  }
  public getAll(): void {
    this.apiService.getAll().subscribe(
      (data: any) => {
        this.products = data;
        console.log('Product', this.products);

      },
      (err) => {
        this.error = err;
      }
    );
  }
  createOrUpdate(form: any) {
    //  form.value.id = this.selectedProduct.id;
    let prod:any  = {
      "name" : this.selectedProduct.name,
      "description" :this.selectedProduct.description,
      "price" : this.selectedProduct.price,
      //


    };
    if (this.flagSelected) {
      prod["id"] = this.selectedProduct._id;
      console.log( "up",prod);
      this.apiService.update(prod).subscribe(
        (response: any)=>{
          console.log('data',response);

          alert(response.message);
          this.getAll();
        }
      );
    }
    else {
      console.log("Khoa check");
      this.apiService.create(prod).pipe(
        mergeMap((res): any => {
          return this.apiService.getAll().pipe(
            tap((prod: Product[]) => {
              this.products = prod;
            })
          )
        })
      ).subscribe((response: any)=>{
        alert("Create user successully!");
        this.products = response;
      });
    }
  }

  select(product: Product) {
    this.selectedProduct = product;
    this.flagSelected = true;
   // this.show= !this.show;
  }

  deletemploy(id: any) {
    this.apiService.delete(id).subscribe((response: any) => {
      alert(response['message']);
      this.getAll();
    });
  }
  public add(): void {
    this.show= !this.show;
  }
}
