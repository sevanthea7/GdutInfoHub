// src/mock/mockAcademicData.d.ts
declare module "@/mock/mockAcademicData" {
  export interface AcademicItem {
    title: string;
    url: string;
    date: string;
    content: string;
    key_words: string[];
    department: string;
  }

  export interface MockAcademicData {
    code: number;
    msg: string;
    data: {
      items: AcademicItem[];
    };
  }

  export const mockNoticeData: MockAcademicData;
}
