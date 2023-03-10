import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PositionalIndexComponent } from './positional-index.component';

describe('PositionalIndexComponent', () => {
  let component: PositionalIndexComponent;
  let fixture: ComponentFixture<PositionalIndexComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PositionalIndexComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PositionalIndexComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
