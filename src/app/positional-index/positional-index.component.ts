import { Component, ViewChild } from '@angular/core';
import { Med, MedService } from '../med.service';
import { HttpClient } from '@angular/common/http';
import { Table } from 'primeng/table';
import { DataView } from 'primeng/dataview';
@Component({
  selector: 'app-positional-index',
  templateUrl: './positional-index.component.html',
  providers: [MedService, HttpClient],
  styleUrls: ['./positional-index.component.scss']
})



export class PositionalIndexComponent {
  totalRecords: number = 0;
  phrase: string = '';
  meds: Med[] = [];
  first: number = 0;
  rows: number = 9;
  loading: boolean = true;
  private timeout?: number;
  @ViewChild('dv') dv: DataView | undefined;
  constructor(private medService: MedService) { }
  ngOnInit(): void {
    
    this.medService.getMed(this.first, this.rows, this.phrase).subscribe((meds) => {
      this.meds = meds.data;
      this.totalRecords = meds.total;
      this.loading = false;
    });
  }

  loadData(event: any) {
    this.loading = true;
    this.medService.getMed(event.first, event.rows, this.phrase).subscribe((meds) => {
      this.meds = meds.data;
      this.totalRecords = meds.total;
      this.loading = false;
    });
  }

  searchPhrase($event: any) {
    window.clearTimeout(this.timeout);
    this.timeout = window.setTimeout(() => {

    this.phrase = (($event.target as HTMLInputElement).value);
    
    this.loadData({ first: 0, rows: this.rows });
    }, 300);
  }
    



}
