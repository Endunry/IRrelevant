import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PositionalIndexComponent } from './positional-index/positional-index.component';

const routes: Routes = [
  {
    path: 'positional-index',
    component: PositionalIndexComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
