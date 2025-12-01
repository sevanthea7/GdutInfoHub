// src/mock/mockLogisticsRepaircData.d.ts
declare module "@/mock/mockLogisticsRepairData" {
  export interface LogisticsItem {
    title: string;
    url: string;
    date: string;
    content: string;
    key_words: string[];
    department: string;
  }

  export interface MockLogisticsRepairData {
    code: number;
    msg: string;
    data: {
      items: LogisticsItem[];
    };
  }

  export const mockNoticeData: MockLogisticsRepairData;
}
