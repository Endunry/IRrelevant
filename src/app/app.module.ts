import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { DataViewModule } from 'primeng/dataview';
import { PaginatorModule } from 'primeng/paginator';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { InputTextModule } from 'primeng/inputtext';
import { ShellComponent } from './shell/shell.component';
import { PositionalIndexComponent } from './positional-index/positional-index.component';
import { HttpClient, HttpClientModule, HttpHandler } from '@angular/common/http';

@NgModule({
  declarations: [
    AppComponent,
    ShellComponent,
    PositionalIndexComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    PaginatorModule,
    DataViewModule,
    HttpClientModule,
    InputTextModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
