// src/mock/mockNoticeData.d.ts
declare module "@/mock/mockNoticeData" {
  export interface NoticeItem {
    title: string;
    url: string;
    date: string;
    content: string;
    key_words: string[];
    label: string;
    department: string;
  }

  export interface MockNoticeData {
    code: number;
    msg: string;
    data: {
      items: NoticeItem[];
    };
  }

  export const mockNoticeData: MockNoticeData;
}
