export interface BlockedNumber {
  id: string;
  number: string;
  date: string;
  caller?: string;
  type: 'spam' | 'telemarketer' | 'scam' | 'unknown';
}

export interface BlockedNumberCardProps {
  count: number;
  todayCount: number;
}

export interface NumberListItemProps {
  item: BlockedNumber;
}

export interface ActionButtonProps {
  running: boolean;
  onPress: () => void;
  btnName: string
}
