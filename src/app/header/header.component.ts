import { Component } from '@angular/core';
import { MenuItem } from 'primeng/api';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {

  menuModel: MenuItem[] = [
    {
      label: 'PosIndex',
      icon: 'pi pi-fw pi-book',
      routerLink: 'positional-index'
    },
  ]
  constructor() { }
}
