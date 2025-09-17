import { Ref } from 'vue'

export function TableEntry<T>(array: Array<T>, refValue: Ref<T[]>) {
  // Generic composable for table-like data
  return {
    array,
    refValue,
  }
}
