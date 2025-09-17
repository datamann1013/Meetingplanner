import { ref } from 'vue'

export function EventActions(initialAction: string, actions: string[], emit: (event: string, ...args: any[]) => void) {
  const selectedAction = ref<string>(initialAction ?? actions[0])

  function selectAction(action: string) {
    selectedAction.value = action
    emit('updateAction', action)
  }

  return {
    actions,
    selectedAction,
    selectAction,
  }
}
