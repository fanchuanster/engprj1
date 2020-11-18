import { TestBed } from '@angular/core/testing';

import { MrService } from './mr.service';

describe('MrService', () => {
  let service: MrService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MrService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
