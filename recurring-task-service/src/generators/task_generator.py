"""
Task Generator for the Recurring Task Service
Generates recurring task instances based on templates
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List
from dateutil.rrule import rrulestr
from dateutil.parser import parse
import uuid

logger = logging.getLogger(__name__)


class TaskGenerator:
    def __init__(self):
        pass

    async def generate_tasks(self, template_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate recurring task instances based on the template and recurrence rule
        """
        try:
            # Extract template information
            base_task = template_data.get('base_task', {})
            recurrence_rule = template_data.get('recurrence_rule')
            start_date = template_data.get('start_date')
            ends_on = template_data.get('ends_on')
            occurrence_count = template_data.get('occurrence_count')

            if not recurrence_rule:
                logger.error("Recurrence rule is required to generate tasks")
                return []

            # Parse the recurrence rule using dateutil
            rule = rrulestr(recurrence_rule)

            # Set the start date for the rule
            if start_date:
                rule.after(parse(start_date))

            # Generate task instances based on the rule
            generated_tasks = []
            count = 0

            for dt in rule:
                # Stop if we've reached the occurrence limit
                if occurrence_count and count >= occurrence_count:
                    break

                # Stop if we've passed the end date
                if ends_on and dt.datetime() > parse(ends_on):
                    break

                # Create a new task instance based on the base task
                new_task = self.create_task_instance(base_task, dt.datetime())
                generated_tasks.append(new_task)
                count += 1

                # Limit the number of tasks to prevent infinite loops
                if count > 100:  # Reasonable limit for safety
                    logger.warning("Reached maximum task generation limit (100)")
                    break

            logger.info(f"Generated {len(generated_tasks)} recurring task instances")
            return generated_tasks

        except Exception as e:
            logger.error(f"Error generating recurring tasks: {str(e)}")
            return []

    def create_task_instance(self, base_task: Dict[str, Any], scheduled_date: datetime) -> Dict[str, Any]:
        """
        Create a new task instance based on the base task and scheduled date
        """
        # Copy the base task properties
        new_task = base_task.copy()

        # Generate a new ID for the instance
        new_task['id'] = str(uuid.uuid4())

        # Set the scheduled date as the due date for this instance
        new_task['due_date'] = scheduled_date.isoformat()

        # Mark as pending status
        new_task['status'] = 'pending'

        # Set creation date
        new_task['created_at'] = datetime.now().isoformat()
        new_task['updated_at'] = datetime.now().isoformat()

        # Link back to the parent template
        new_task['parent_task_id'] = base_task.get('id')

        # Reset completion date
        new_task['completed_at'] = None

        # Modify the title to indicate it's a recurring instance
        if 'title' in new_task:
            new_task['title'] = f"{base_task['title']} - {scheduled_date.strftime('%Y-%m-%d')}"

        return new_task

    async def validate_recurrence_rule(self, recurrence_rule: str) -> bool:
        """
        Validate that the recurrence rule is properly formatted
        """
        try:
            rrulestr(recurrence_rule)
            return True
        except Exception:
            return False

    async def get_next_occurrence(self, recurrence_rule: str, start_date: datetime) -> datetime:
        """
        Get the next occurrence date based on the recurrence rule
        """
        try:
            rule = rrulestr(recurrence_rule)
            next_occurrence = rule.after(start_date)
            return next_occurrence
        except Exception as e:
            logger.error(f"Error calculating next occurrence: {str(e)}")
            return None