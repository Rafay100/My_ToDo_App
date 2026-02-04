import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';
import {
  Calendar,
  Flag,
  Repeat,
  Tag,
  MoreHorizontal,
  Clock,
  Check,
  Star,
  Flame,
  RotateCcw
} from 'lucide-react';
import { format, isToday, isTomorrow, differenceInDays } from 'date-fns';

interface TaskCardProps {
  task: {
    id: string;
    title: string;
    description?: string;
    isCompleted: boolean;
    priority: 'low' | 'medium' | 'high' | 'urgent';
    dueDate?: string; // ISO string
    tags?: string[];
    isRecurring?: boolean;
    createdAt: string;
  };
  onToggleComplete: (id: string, completed: boolean) => void;
  onEdit?: (id: string) => void;
  onDelete?: (id: string) => void;
}

export default function TaskCard({
  task,
  onToggleComplete,
  onEdit,
  onDelete
}: TaskCardProps) {
  const [isHovered, setIsHovered] = useState(false);

  // Calculate days until due
  const daysUntilDue = task.dueDate ? differenceInDays(new Date(task.dueDate), new Date()) : null;

  // Format due date display
  const formatDateDisplay = (dateString?: string) => {
    if (!dateString) return '';

    const date = new Date(dateString);

    if (isToday(date)) return 'Today';
    if (isTomorrow(date)) return 'Tomorrow';

    return format(date, 'MMM dd');
  };

  // Get priority color
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'red';
      case 'high': return 'orange';
      case 'medium': return 'yellow';
      case 'low': return 'green';
      default: return 'gray';
    }
  };

  // Get priority icon
  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case 'urgent':
        return <Flame className="h-3 w-3 text-red-500" />;
      case 'high':
        return <Flag className="h-3 w-3 text-orange-500" />;
      case 'medium':
        return <Star className="h-3 w-3 text-yellow-500" />;
      case 'low':
        return <Flag className="h-3 w-3 text-green-500" />;
      default:
        return <Flag className="h-3 w-3 text-gray-400" />;
    }
  };

  // Get urgency class
  const getUrgencyClass = () => {
    if (!daysUntilDue) return '';
    if (daysUntilDue < 0) return 'text-destructive bg-destructive/10';
    if (daysUntilDue === 0) return 'text-red-600 bg-red-500/10';
    if (daysUntilDue === 1) return 'text-orange-600 bg-orange-500/10';
    if (daysUntilDue <= 3) return 'text-yellow-600 bg-yellow-500/10';
    return 'text-muted-foreground';
  };

  return (
    <div
      className={`group relative bg-card rounded-xl border p-4 transition-all duration-200 hover:shadow-md hover:border-primary/20 ${
        task.isCompleted
          ? 'opacity-70 bg-muted/30'
          : 'hover:bg-accent/50'
      }`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="flex items-start gap-3">
        <div className="pt-0.5">
          <Checkbox
            checked={task.isCompleted}
            onCheckedChange={(checked) => onToggleComplete(task.id, !!checked)}
            className="h-4 w-4 rounded-full border-2 data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground"
          />
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <h3
              className={`text-base font-medium break-words ${
                task.isCompleted
                  ? 'line-through text-muted-foreground'
                  : 'text-foreground'
              }`}
            >
              {task.title}
            </h3>

            <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
              {onEdit && (
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-6 w-6 text-muted-foreground hover:text-foreground"
                  onClick={() => onEdit(task.id)}
                >
                  <MoreHorizontal className="h-3.5 w-3.5" />
                </Button>
              )}
              {onDelete && (
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-6 w-6 text-muted-foreground hover:text-destructive"
                  onClick={() => onDelete(task.id)}
                >
                  <RotateCcw className="h-3.5 w-3.5" />
                </Button>
              )}
            </div>
          </div>

          {task.description && (
            <p className={`text-sm mt-1 text-muted-foreground ${task.isCompleted ? 'line-through' : ''}`}>
              {task.description}
            </p>
          )}

          <div className="flex flex-wrap items-center gap-2 mt-3">
            {/* Priority badge */}
            <Badge
              variant="outline"
              className={`h-6 px-2 text-xs capitalize ${
                task.priority === 'urgent' ? 'border-red-500 text-red-500' :
                task.priority === 'high' ? 'border-orange-500 text-orange-500' :
                task.priority === 'medium' ? 'border-yellow-500 text-yellow-500' :
                task.priority === 'low' ? 'border-green-500 text-green-500' :
                'border-gray-500 text-gray-500'
              }`}
            >
              {getPriorityIcon(task.priority)}
              <span className="ml-1 capitalize">{task.priority}</span>
            </Badge>

            {/* Due date badge */}
            {task.dueDate && (
              <Badge
                variant="outline"
                className={`h-6 px-2 text-xs ${getUrgencyClass()} border-current`}
              >
                <Calendar className="h-3 w-3 mr-1" />
                {formatDateDisplay(task.dueDate)}
                {daysUntilDue !== null && daysUntilDue <= 3 && daysUntilDue >= 0 && (
                  <span className="ml-1">({daysUntilDue === 0 ? 'today' : `${daysUntilDue}d`})</span>
                )}
              </Badge>
            )}

            {/* Recurring badge */}
            {task.isRecurring && (
              <Badge variant="outline" className="h-6 px-2 text-xs">
                <Repeat className="h-3 w-3 mr-1" />
                Recurring
              </Badge>
            )}

            {/* Tags */}
            {task.tags && task.tags.map((tag, index) => (
              <Badge key={index} variant="secondary" className="h-6 px-2 text-xs">
                <Tag className="h-2.5 w-2.5 mr-1" />
                {tag}
              </Badge>
            ))}
          </div>
        </div>
      </div>

      {/* Progress bar for recurring tasks */}
      {task.isRecurring && (
        <div className="mt-3 pt-3 border-t border-muted">
          <div className="flex items-center justify-between text-xs text-muted-foreground mb-1">
            <span>Progress</span>
            <span>60%</span>
          </div>
          <div className="w-full bg-muted rounded-full h-1.5">
            <div className="bg-primary h-1.5 rounded-full w-3/5"></div>
          </div>
        </div>
      )}
    </div>
  );
}