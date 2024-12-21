import { BlockedNumber } from "./type";

export const BLOCKED_NUMBERS: BlockedNumber[] = [
  {
    id: '1',
    number: '+1 (234) 567-8901',
    date: '2024-12-20',
    caller: 'Suspected Telemarketer',
    type: 'telemarketer'
  },
  {
    id: '2',
    number: '+1 (345) 678-9012',
    date: '2024-12-20',
    caller: 'Spam Caller',
    type: 'spam'
  },
  {
    id: '3',
    number: '+1 (456) 789-0123',
    date: '2024-12-19',
    caller: 'Potential Scammer',
    type: 'scam'
  },
  {
    id: '4',
    number: '+1 (567) 890-1234',
    date: '2024-12-19',
    type: 'unknown'
  },
  {
    id: '5',
    number: '+1 (678) 901-2345',
    date: '2024-12-18',
    caller: 'Telemarketing Company',
    type: 'telemarketer'
  },
  {
    id: '6',
    number: '+1 (789) 012-3456',
    date: '2024-12-18',
    type: 'spam'
  },
  {
    id: '7',
    number: '+1 (890) 123-4567',
    date: '2024-12-17',
    caller: 'Known Scammer',
    type: 'scam'
  },
  {
    id: '8',
    number: '+1 (901) 234-5678',
    date: '2024-12-17',
    type: 'unknown',
  },
];
export const STAR_PROTECTION ='Start Recording';
export const STOP_PROTECTION ='Stop Recording';

