# Schedule — Project Alpha (Baseline vs Actual)

Data date: 2025-08-27
Unit: THB

Columns:
- WBS, TaskID, TaskName, BaselineStart, BaselineFinish, Start, Finish, DurationDays
- Predecessors, PercentComplete, Resource, BAC_THB, AC_ToDate_THB
- ActualStart, ActualFinish, Notes

| WBS | TaskID | TaskName                       | BaselineStart | BaselineFinish | Start      | Finish     | DurationDays | Predecessors | PercentComplete | Resource      | BAC_THB | AC_ToDate_THB | ActualStart | ActualFinish | Notes                                 |
|-----|--------|--------------------------------|---------------|----------------|------------|------------|--------------|--------------|-----------------|---------------|---------|----------------|-------------|--------------|---------------------------------------|
| 1.0 | T001   | Project Initiation             | 2025-07-01    | 2025-07-05     | 2025-07-01 | 2025-07-06 | 5            | -            | 100%            | PM Team       | 200,000 | 210,000        | 2025-07-01  | 2025-07-06   | Finished +1 day over baseline         |
| 1.1 | T002   | Design & Permitting            | 2025-07-06    | 2025-08-10     | 2025-07-06 | 2025-08-20 | 36           | T001         | 80%             | Design        | 800,000 | 820,000        | 2025-07-06  | -            | Delayed finish vs baseline            |
| 2.0 | T003   | Site Preparation               | 2025-08-01    | 2025-08-15     | 2025-08-03 | 2025-08-28 | 15           | T002         | 60%             | Civil         | 500,000 | 450,000        | 2025-08-03  | -            | Late start; progress ongoing          |
| 3.0 | T004   | Foundation                     | 2025-08-16    | 2025-09-15     | 2025-08-20 | 2025-09-25 | 31           | T003         | 30%             | Civil         | 1,500,000 | 400,000       | 2025-08-20  | -            | Started later; behind baseline        |
| 4.0 | T005   | Structure - Ground Floor       | 2025-09-16    | 2025-10-15     | 2025-09-16 | 2025-10-20 | 30           | T004         | 0%              | Structure     | 2,000,000 | 0            | -           | -            | Not started yet                       |
| 4.1 | T006   | Structure - Upper Floors       | 2025-10-16    | 2025-11-30     | 2025-10-16 | 2025-12-05 | 46           | T005         | 0%              | Structure     | 3,000,000 | 0            | -           | -            | Not started yet                       |
| 5.0 | T007   | MEP Rough-in                   | 2025-11-01    | 2025-12-15     | 2025-11-01 | 2025-12-20 | 45           | T006         | 0%              | MEP           | 1,200,000 | 0            | -           | -            | Planned after structure               |
| 6.0 | T008   | Enclosure (Façade & Roofing)   | 2025-11-15    | 2025-12-31     | 2025-11-15 | 2026-01-05 | 47           | T006         | 0%              | Envelope      | 1,400,000 | 0            | -           | -            | Planned after structure               |
| 7.0 | T009   | Interior Fit-out               | 2025-12-01    | 2026-01-20     | 2025-12-01 | 2026-01-25 | 51           | T007,T008    | 0%              | Fitout        | 2,200,000 | 0            | -           | -            | Depends on MEP & Enclosure            |
| 8.0 | T010   | Testing & Commissioning        | 2026-01-21    | 2026-01-31     | 2026-01-21 | 2026-02-02 | 11           | T009         | 0%              | Commissioning | 300,000 | 0              | -           | -            | Final stage                           |

Notes:
- DurationDays อ้างอิงตามช่วง Start–Finish ที่วางไว้ (ไม่รวมวันหยุด/constraint เพิ่มเติม)
- BAC_THB คืองบตามแผนต่อกิจกรรม (Budget at Completion)